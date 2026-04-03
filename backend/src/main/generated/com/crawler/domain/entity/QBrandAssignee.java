package com.crawler.domain.entity;

import static com.querydsl.core.types.PathMetadataFactory.*;

import com.querydsl.core.types.dsl.*;

import com.querydsl.core.types.PathMetadata;
import javax.annotation.processing.Generated;
import com.querydsl.core.types.Path;
import com.querydsl.core.types.dsl.PathInits;


/**
 * QBrandAssignee is a Querydsl query type for BrandAssignee
 */
@Generated("com.querydsl.codegen.DefaultEntitySerializer")
public class QBrandAssignee extends EntityPathBase<BrandAssignee> {

    private static final long serialVersionUID = -1240032082L;

    private static final PathInits INITS = PathInits.DIRECT2;

    public static final QBrandAssignee brandAssignee = new QBrandAssignee("brandAssignee");

    public final StringPath accountId = createString("accountId");

    public final BooleanPath active = createBoolean("active");

    public final NumberPath<Long> assigneeId = createNumber("assigneeId", Long.class);

    public final StringPath assigneeName = createString("assigneeName");

    public final QBrand brand;

    public final DateTimePath<java.time.LocalDateTime> createdAt = createDateTime("createdAt", java.time.LocalDateTime.class);

    public final StringPath platformId = createString("platformId");

    public final DateTimePath<java.time.LocalDateTime> updatedAt = createDateTime("updatedAt", java.time.LocalDateTime.class);

    public QBrandAssignee(String variable) {
        this(BrandAssignee.class, forVariable(variable), INITS);
    }

    public QBrandAssignee(Path<? extends BrandAssignee> path) {
        this(path.getType(), path.getMetadata(), PathInits.getFor(path.getMetadata(), INITS));
    }

    public QBrandAssignee(PathMetadata metadata) {
        this(metadata, PathInits.getFor(metadata, INITS));
    }

    public QBrandAssignee(PathMetadata metadata, PathInits inits) {
        this(BrandAssignee.class, metadata, inits);
    }

    public QBrandAssignee(Class<? extends BrandAssignee> type, PathMetadata metadata, PathInits inits) {
        super(type, metadata, inits);
        this.brand = inits.isInitialized("brand") ? new QBrand(forProperty("brand")) : null;
    }

}

